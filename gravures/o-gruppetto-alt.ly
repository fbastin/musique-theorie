\version "2.24.3"
%% Fichier produit par outils/generer_ornements.py — ne pas modifier à la main.
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
      \key c \major g'4\turn g'4-\tweak self-alignment-X #CENTER ^\markup \override #'(baseline-skip . 1.9) \center-column { \musicglyph "scripts.turn" \teeny \sharp }
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic "joué" } {
      \clef treble \time 2/4 \autoBeamOff
      \key c \major a'16[ g'16 f'16 g'16] a'16[ g'16 fis'16 g'16]
      \bar "|."
    }
  >>
  \layout {
    indent = 17\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
