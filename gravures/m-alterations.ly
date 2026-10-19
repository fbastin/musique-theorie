\version "2.24.3"
%% Fichier produit par outils/generer_mordants.py — ne pas modifier à la main.
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
  \new StaffGroup <<
    \new Staff \with { instrumentName = \markup \small \italic "écrit" } {
      \clef treble \time 2/4
      \key c \major g'2\mordent | g'2-\tweak self-alignment-X #CENTER ^\markup \override #'(baseline-skip . 1.9) \center-column { \musicglyph "scripts.mordent" \teeny \sharp } | \key g \major g'2\mordent
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic "joué" } {
      \clef treble \time 2/4 \autoBeamOff
      \key c \major g'32[ f'32]_\markup \tiny \italic "ton" g'4.. | g'32[ fis'32]_\markup \tiny \italic "demi-ton" g'4.. | \key g \major g'32[ fis'32]_\markup \tiny \italic "demi-ton" g'4..
      \bar "|."
    }
  >>
  \layout {
    indent = 17\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
