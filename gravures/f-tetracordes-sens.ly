\version "2.24.3"
%% Fichier produit par outils/generer.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  <<
    \new Staff \with { instrumentName = \markup \small \italic "majeur" } <<
      \new Voice {
        \override TextScript.staff-padding = #2.5
        \accidentalStyle forget
        \clef treble
        \omit Staff.TimeSignature
        \cadenzaOn
        \key c \major
        c'4^\markup \small \italic "en montant" d'4 e'4 f'4 \bar "||" f'4^\markup \small \italic "en descendant" e'4 d'4 c'4 \bar "|."
      }
      \new NullVoice = "pas-majeur" { \cadenzaOn s8 c'4 c'4 c'4 s8 s8 c'4 c'4 c'4 s8 }
    >>
    \new Lyrics \with {
      \override LyricText.font-size = #-2
      \override LyricText.font-shape = #'italic
      % À la même hauteur sous les deux portées.
      \override VerticalAxisGroup.nonstaff-relatedstaff-spacing =
        #'((basic-distance . 5.5) (minimum-distance . 5.5) (padding . 0.5) (stretchability . 0))
    } \lyricsto "pas-majeur" { "ton" "ton" "½ ton" "½ ton" "ton" "ton" }
    \new Staff \with { instrumentName = \markup \small \italic "phrygien" } <<
      \new Voice {
        \override TextScript.staff-padding = #2.5
        \accidentalStyle forget
        \clef treble
        \omit Staff.TimeSignature
        \cadenzaOn
        \key c \major
        c'4 des'4 ees'4 f'4 \bar "||" f'4 ees'4 des'4 c'4 \bar "|."
      }
      \new NullVoice = "pas-phrygien" { \cadenzaOn s8 c'4 c'4 c'4 s8 s8 c'4 c'4 c'4 s8 }
    >>
    \new Lyrics \with {
      \override LyricText.font-size = #-2
      \override LyricText.font-shape = #'italic
      % À la même hauteur sous les deux portées.
      \override VerticalAxisGroup.nonstaff-relatedstaff-spacing =
        #'((basic-distance . 5.5) (minimum-distance . 5.5) (padding . 0.5) (stretchability . 0))
    } \lyricsto "pas-phrygien" { "½ ton" "ton" "ton" "ton" "ton" "½ ton" }
  >>
  \layout {
    indent = 15\mm
    \context {
      \Score
      %% Un espacement proportionnel : les noires à égale distance, et un
      %% nom d'intervalle, à mi-chemin, entre chaque paire.
      proportionalNotationDuration = #(ly:make-moment 1/12)
      \override SpacingSpanner.uniform-stretching = ##t
    }
  }
}
