\version "2.24.3"
%% Fichier produit par outils/generer.py — ne pas modifier à la main.
#(set-global-staff-size 24)
\paper {
  indent = 0
  ragged-right = ##f
  %% Les trois doivent s'accorder : LilyPond rejette une largeur de ligne qui ne
  %% s'ajuste pas aux marges et revient silencieusement à ses valeurs par défaut
  %% (« margins do not fit with line-width »). D'où la largeur de page explicite.
  paper-width = 81\mm
  line-width = 79\mm
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
  \new Staff {
    \clef treble
    \key c \major
    \omit Staff.TimeSignature
    \cadenzaOn
    c' d' e' f' g' a' b' c''
    \bar "|."
  }
  \layout { }
}
